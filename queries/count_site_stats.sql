-- :name count_site_stats :many

SELECT
	site_id,
    count(IF(first_snapshot_at = snapshot_at, 1, NULL)) as discover_count,
    count(IF(first_snapshot_at != snapshot_at, 1, NULL)) as update_count
FROM
(
	SELECT
		ArticleSnapshot.article_id, Article.site_id, Article.first_snapshot_at, ArticleSnapshot.snapshot_at
	FROM
		ArticleSnapshot
	INNER JOIN
		Article
	ON
		ArticleSnapshot.article_id = Article.article_id
	WHERE
		ArticleSnapshot.snapshot_at >= :time_start
	AND
		ArticleSnapshot.snapshot_at < :time_end
) as T
group by site_id