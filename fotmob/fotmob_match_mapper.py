"""Map Understat matches to FotMob match ids.

The primary lookup uses FotMob's public daily matches endpoint:
https://www.fotmob.com/api/matches?date=YYYYMMDD

Examples:
    python fotmob/fotmob_match_mapper.py --home "Manchester United" --away Fulham --date 2024-08-16
    python fotmob/fotmob_match_mapper.py --transport playwright --home "Manchester United" --away Fulham --date 2024-08-16
    python fotmob/fotmob_match_mapper.py --cache-file 47_matches_by_date.rds --home "Manchester United" --away Fulham --date 2024-08-16
    python fotmob/fotmob_match_mapper.py --input-csv matches.csv --output-csv mapped.csv
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


FOTMOB_MATCHES_URL = "https://www.fotmob.com/api/matches"
DEFAULT_MIN_CONFIDENCE = 0.92

TEAM_ALIASES = {
    "afc bournemouth": "bournemouth",
    "bournemouth": "bournemouth",
    "arsenal": "arsenal",
    "aston villa": "aston villa",
    "brentford": "brentford",
    "brighton": "brighton",
    "brighton and hove albion": "brighton",
    "chelsea": "chelsea",
    "crystal palace": "crystal palace",
    "everton": "everton",
    "fulham": "fulham",
    "ipswich": "ipswich",
    "ipswich town": "ipswich",
    "leicester": "leicester",
    "leicester city": "leicester",
    "liverpool": "liverpool",
    "man city": "manchester city",
    "manchester city": "manchester city",
    "man united": "manchester united",
    "manchester united": "manchester united",
    "man utd": "manchester united",
    "newcastle": "newcastle united",
    "newcastle united": "newcastle united",
    "nottingham forest": "nottingham forest",
    "nottm forest": "nottingham forest",
    "southampton": "southampton",
    "tottenham": "tottenham",
    "tottenham hotspur": "tottenham",
    "spurs": "tottenham",
    "west ham": "west ham",
    "west ham united": "west ham",
    "wolves": "wolves",
    "wolverhampton": "wolves",
    "wolverhampton wanderers": "wolves",
}


@dataclass(frozen=True)
class MatchCandidate:
    fotmob_match_id: int
    home_team: str
    away_team: str
    league_name: str | None
    match_time_utc: str | None
    status: str | None
    score: float
    home_score: float
    away_score: float


def normalize_team_name(value: str) -> str:
    text = unicodedata.normalize("NFKD", value or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\b(fc|afc|cf)\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return TEAM_ALIASES.get(text, text)


def similarity(left: str, right: str) -> float:
    left_norm = normalize_team_name(left)
    right_norm = normalize_team_name(right)
    if left_norm == right_norm:
        return 1.0
    return SequenceMatcher(None, left_norm, right_norm).ratio()


def parse_match_date(value: str | dt.date) -> dt.date:
    if isinstance(value, dt.date):
        return value
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%Y%m%d", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {value!r}")


def fotmob_matches_url(match_date: str | dt.date) -> str:
    date_value = parse_match_date(match_date).strftime("%Y%m%d")
    return f"{FOTMOB_MATCHES_URL}?{urlencode({'date': date_value})}"


def fetch_fotmob_matches_direct(match_date: str | dt.date, timeout: int = 30) -> dict[str, Any]:
    url = fotmob_matches_url(match_date)
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0 Safari/537.36"
            ),
        },
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"FotMob HTTP {exc.code} for {url}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach FotMob endpoint {url}: {exc}") from exc

    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        preview = body[:500].replace("\n", " ")
        raise RuntimeError(f"FotMob returned non-JSON content for {url}: {preview}") from exc

    return payload


def fetch_fotmob_matches_playwright(match_date: str | dt.date, timeout: int = 30) -> dict[str, Any]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright is not installed. Use --transport direct or install playwright.") from exc

    url = fotmob_matches_url(match_date)
    path = "/api/matches?" + urlencode({"date": parse_match_date(match_date).strftime("%Y%m%d")})
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(
            extra_http_headers={
                "Accept": "application/json",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0 Safari/537.36"
                ),
            }
        )
        page.goto("https://www.fotmob.com", wait_until="domcontentloaded", timeout=timeout * 1000)
        result = page.evaluate(
            """async (path) => {
                const response = await fetch(path, {headers: {Accept: 'application/json'}});
                return {status: response.status, text: await response.text()};
            }""",
            path,
        )
        browser.close()

    if result["status"] >= 400:
        detail = result["text"][:500]
        raise RuntimeError(f"FotMob HTTP {result['status']} for {url}: {detail}")
    try:
        return json.loads(result["text"])
    except json.JSONDecodeError as exc:
        preview = result["text"][:500].replace("\n", " ")
        raise RuntimeError(f"FotMob returned non-JSON content for {url}: {preview}") from exc


def fetch_fotmob_matches(
    match_date: str | dt.date,
    timeout: int = 30,
    transport: str = "auto",
) -> dict[str, Any]:
    if transport == "direct":
        return fetch_fotmob_matches_direct(match_date, timeout)
    if transport == "playwright":
        return fetch_fotmob_matches_playwright(match_date, timeout)
    if transport != "auto":
        raise ValueError(f"Unsupported transport: {transport!r}")

    try:
        return fetch_fotmob_matches_direct(match_date, timeout)
    except RuntimeError as direct_error:
        try:
            return fetch_fotmob_matches_playwright(match_date, timeout)
        except RuntimeError as playwright_error:
            raise RuntimeError(
                "FotMob lookup failed with direct HTTP and Playwright transports. "
                f"direct={direct_error}; playwright={playwright_error}"
            ) from playwright_error


def iter_matches(payload: dict[str, Any]) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for league in payload.get("leagues", []):
        league_name = league.get("name") or league.get("localizedName")
        for match in league.get("matches", []):
            enriched = dict(match)
            enriched["_league_name"] = league_name
            matches.append(enriched)
    return matches


def extract_team_name(team_value: Any) -> str:
    if isinstance(team_value, dict):
        return str(team_value.get("name") or team_value.get("shortName") or "")
    return str(team_value or "")


def extract_match_id(match: dict[str, Any]) -> int | None:
    for key in ("id", "matchId", "pageUrl"):
        value = match.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            digits = re.findall(r"\d+", value)
            if digits:
                return int(digits[-1])
    return None


def extract_time(match: dict[str, Any]) -> str | None:
    status = match.get("status")
    if isinstance(status, dict):
        utc_time = status.get("utcTime")
        if utc_time:
            return str(utc_time)
    for key in ("time", "matchTimeUTC", "utcTime"):
        if match.get(key):
            return str(match[key])
    return None


def build_candidates(
    home_team: str,
    away_team: str,
    payload: dict[str, Any],
) -> list[MatchCandidate]:
    candidates: list[MatchCandidate] = []
    for match in iter_matches(payload):
        match_id = extract_match_id(match)
        if match_id is None:
            continue

        home = extract_team_name(match.get("home") or match.get("homeTeam"))
        away = extract_team_name(match.get("away") or match.get("awayTeam"))
        if not home or not away:
            continue

        home_score = similarity(home_team, home)
        away_score = similarity(away_team, away)
        score = (home_score + away_score) / 2
        status = match.get("status")
        status_text = status.get("reason", {}).get("short") if isinstance(status, dict) else None

        candidates.append(
            MatchCandidate(
                fotmob_match_id=match_id,
                home_team=home,
                away_team=away,
                league_name=match.get("_league_name"),
                match_time_utc=extract_time(match),
                status=status_text,
                score=round(score, 4),
                home_score=round(home_score, 4),
                away_score=round(away_score, 4),
            )
        )

    return sorted(candidates, key=lambda item: item.score, reverse=True)


def load_cache_rows(cache_file: str, match_date: str | dt.date) -> list[dict[str, Any]]:
    date_text = parse_match_date(match_date).isoformat()
    if cache_file.lower().endswith(".rds"):
        try:
            import pyreadr  # type: ignore
        except ImportError as exc:
            raise RuntimeError("pyreadr is required to read RDS cache files.") from exc

        result = pyreadr.read_r(cache_file)
        dataframe = next(iter(result.values()))
        rows = dataframe.to_dict(orient="records")
    else:
        with open(cache_file, newline="", encoding="utf-8-sig") as input_file:
            rows = list(csv.DictReader(input_file))

    return [row for row in rows if str(row.get("date") or row.get("match_date"))[:10] == date_text]


def build_candidates_from_cache(
    home_team: str,
    away_team: str,
    rows: list[dict[str, Any]],
) -> list[MatchCandidate]:
    candidates: list[MatchCandidate] = []
    for row in rows:
        match_id = row.get("match_id") or row.get("fotmob_match_id")
        if match_id is None or str(match_id) == "nan":
            continue

        home = str(row.get("home_name") or row.get("home_team") or row.get("home") or "")
        away = str(row.get("away_name") or row.get("away_team") or row.get("away") or "")
        if not home or not away:
            continue

        home_score = similarity(home_team, home)
        away_score = similarity(away_team, away)
        score = (home_score + away_score) / 2

        candidates.append(
            MatchCandidate(
                fotmob_match_id=int(float(match_id)),
                home_team=home,
                away_team=away,
                league_name=row.get("name") or row.get("league_name"),
                match_time_utc=row.get("match_status_utc_time") or row.get("match_time_utc"),
                status=row.get("match_status_score_str") or row.get("status"),
                score=round(score, 4),
                home_score=round(home_score, 4),
                away_score=round(away_score, 4),
            )
        )

    return sorted(candidates, key=lambda item: item.score, reverse=True)


def map_match(
    home_team: str,
    away_team: str,
    match_date: str | dt.date,
    min_confidence: float = DEFAULT_MIN_CONFIDENCE,
    timeout: int = 30,
    transport: str = "auto",
    cache_file: str | None = None,
) -> dict[str, Any]:
    if cache_file:
        candidates = build_candidates_from_cache(home_team, away_team, load_cache_rows(cache_file, match_date))
        method = "fotmob_cached_matches_by_date_and_team_names"
    else:
        payload = fetch_fotmob_matches(match_date, timeout=timeout, transport=transport)
        candidates = build_candidates(home_team, away_team, payload)
        method = "fotmob_daily_matches_by_date_and_team_names"

    selected = candidates[0] if candidates and candidates[0].score >= min_confidence else None

    return {
        "query": {
            "home_team": home_team,
            "away_team": away_team,
            "match_date": parse_match_date(match_date).isoformat(),
        },
        "status": "matched" if selected else "not_matched",
        "fotmob_match_id": selected.fotmob_match_id if selected else None,
        "confidence": selected.score if selected else (candidates[0].score if candidates else 0.0),
        "method": method,
        "candidate_count": len(candidates),
        "selected": asdict(selected) if selected else None,
        "candidates": [asdict(candidate) for candidate in candidates[:10]],
    }


def map_csv(args: argparse.Namespace) -> int:
    with open(args.input_csv, newline="", encoding="utf-8-sig") as input_file:
        rows = list(csv.DictReader(input_file))

    if not rows:
        print("Input CSV is empty.", file=sys.stderr)
        return 1

    output_rows: list[dict[str, Any]] = []
    for row in rows:
        home = row.get("home_team") or row.get("home")
        away = row.get("away_team") or row.get("away")
        date_value = row.get("match_date") or row.get("date")
        if not home or not away or not date_value:
            row["mapper_status"] = "missing_required_fields"
            row["fotmob_match_id"] = ""
            row["mapper_confidence"] = ""
            output_rows.append(row)
            continue

        result = map_match(
            home,
            away,
            date_value,
            args.min_confidence,
            args.timeout,
            args.transport,
            args.cache_file,
        )
        row["fotmob_match_id"] = result["fotmob_match_id"] or ""
        row["mapper_status"] = result["status"]
        row["mapper_confidence"] = result["confidence"]
        output_rows.append(row)

    if args.output_csv:
        fieldnames = list(dict.fromkeys(key for row in output_rows for key in row.keys()))
        with open(args.output_csv, "w", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(output_rows)
    else:
        for row in output_rows:
            print(json.dumps(row, ensure_ascii=False))

    return 0


def add_db_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--database-url", help="Optional PostgreSQL connection string.")
    parser.add_argument("--limit", type=int, help="Limit rows read from matches.")
    parser.add_argument(
        "--update-db",
        action="store_true",
        help="Update matches.fotmob_match_id for matched rows. Requires --database-url.",
    )


def map_database(args: argparse.Namespace) -> int:
    if not args.database_url:
        print("--database-url is required with --from-db.", file=sys.stderr)
        return 1

    try:
        import psycopg  # type: ignore
    except ImportError:
        print("psycopg is not installed. Use --input-csv or install psycopg.", file=sys.stderr)
        return 1

    sql = """
        select understat_match_id, match_date, home_team, away_team
        from matches
        where fotmob_match_id is null
        order by match_date, understat_match_id
    """
    if args.limit:
        sql += " limit %s"
        params: tuple[Any, ...] = (args.limit,)
    else:
        params = ()

    mapped = 0
    processed = 0
    with psycopg.connect(args.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

        for understat_match_id, match_date, home_team, away_team in rows:
            processed += 1
            result = map_match(
                home_team,
                away_team,
                match_date,
                args.min_confidence,
                args.timeout,
                args.transport,
                args.cache_file,
            )
            print(json.dumps({"understat_match_id": understat_match_id, **result}, ensure_ascii=False))

            if args.update_db and result["fotmob_match_id"]:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        update matches
                        set fotmob_match_id = %s
                        where understat_match_id = %s
                        """,
                        (result["fotmob_match_id"], understat_match_id),
                    )
                mapped += 1

        if args.update_db:
            conn.commit()

    print(json.dumps({"processed": processed, "updated": mapped if args.update_db else 0}))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Discover FotMob match ids from date/home/away.")
    parser.add_argument("--home", help="Home team name.")
    parser.add_argument("--away", help="Away team name.")
    parser.add_argument("--date", help="Match date: YYYY-MM-DD, YYYYMMDD, or DD/MM/YYYY.")
    parser.add_argument("--input-csv", help="CSV with home_team, away_team, match_date columns.")
    parser.add_argument("--output-csv", help="Write CSV mapping output.")
    parser.add_argument("--from-db", action="store_true", help="Read pending rows from PostgreSQL matches table.")
    parser.add_argument("--min-confidence", type=float, default=DEFAULT_MIN_CONFIDENCE)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument(
        "--transport",
        choices=("auto", "direct", "playwright"),
        default="auto",
        help="FotMob fetch transport. auto tries direct HTTP, then Playwright.",
    )
    parser.add_argument(
        "--cache-file",
        help="Optional CSV/RDS cache with date, home_name, away_name and match_id columns.",
    )
    add_db_arguments(parser)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.input_csv:
        return map_csv(args)
    if args.from_db:
        return map_database(args)
    if not args.home or not args.away or not args.date:
        parser.error("Provide --home, --away and --date, or use --input-csv/--from-db.")

    result = map_match(
        args.home,
        args.away,
        args.date,
        args.min_confidence,
        args.timeout,
        args.transport,
        args.cache_file,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "matched" else 2


if __name__ == "__main__":
    raise SystemExit(main())
