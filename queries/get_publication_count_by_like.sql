-- :name get_publication_count_by_like :one
SELECT count(*) as publication_count
FROM publication
WHERE title like :query OR publication_text like :query