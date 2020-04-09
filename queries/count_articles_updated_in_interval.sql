-- :name count_articles_updated_in_interval :many
select site_id, count(*) as update_count
from
(
select
ArticleSnapshot.article_id, Article.site_id, Article.first_snapshot_at, ArticleSnapshot.snapshot_at
from ArticleSnapshot, Article
where ArticleSnapshot.article_id = Article.article_id
and DATE(ArticleSnapshot.snapshot_at_date) = :date
) as B
where B.first_snapshot_at != B.snapshot_at
group by A.site_id;