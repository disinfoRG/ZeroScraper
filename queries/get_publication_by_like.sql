-- :name get_publication_by_like :many
SELECT *
FROM publication
WHERE title like :query OR publication_text like :query