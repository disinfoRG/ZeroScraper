from dateutil.parser import parse


def get_stats(queries, args):
    site_id = args.get("site_id", None)
    date = args.get("date", None)
    if site_id:
        site_id = int(site_id)
        site = queries.get_site_by_id(site_id=site_id)
        if site:
            stats = list(queries.get_stats_by_site(site_id=site_id, days=30))
            return {
                "body": {
                    "message": f"Returning stats of site {site_id} from the last 30 days.",
                    "result": stats,
                }
            }

        else:
            return {
                "body": {"message": f"No site with id {site_id}", "result": dict()},
                "status_code": 404,
            }

    elif date:
        date = parse(date).strftime("%Y-%m-%d")
        stats = list(queries.get_stats_by_date(date=date))
        if stats:
            return {
                "body": {
                    "message": f"Return stats of all sites on {date}",
                    "result": stats,
                }
            }
        else:
            return {
                "body": {"message": f"No stats on {date}", "result": {}},
                "status_code": 404,
            }
    else:
        stats = list(queries.get_all_stats())
        return {
            "body": {"message": f"Returning all stats", "result": stats},
            "status_code": 200,
        }
