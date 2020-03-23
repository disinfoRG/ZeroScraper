-- :name get_duplicate_url :many
SELECT url, url_hash, count(*) as count from Article
where site_id = :site_id
group by url;