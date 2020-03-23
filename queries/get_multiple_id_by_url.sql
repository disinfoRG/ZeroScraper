-- :name get_multiple_id_by_url :many
SELECT article_id
FROM Article
WHERE url_hash = :url_hash
order by snapshot_count asc
limit :limit;

