-- :name get_article_latest_snapshot :one
select article_id, snapshot_at, raw_data from ArticleSnapshot
where article_id=:article_id
order by snapshot_at desc
limit 1;