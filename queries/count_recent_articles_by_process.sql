-- :name count_recent_articles_by_process :one
select
COUNT(IF(snapshot_count > 1, 1, NULL)) as `update`,
COUNT(IF(snapshot_count = 1, 1, NULL)) as `discover`
from
(
    select Article.article_id, Article.snapshot_count
    from Article
    inner join ArticleSnapshot
    on Article.article_id = ArticleSnapshot.article_id
    where ArticleSnapshot.snapshot_at > :after
    and Article.article_type="Article"
) as T
