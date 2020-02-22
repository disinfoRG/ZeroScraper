-- :name get_publication_by_like :many
SELECT *
FROM publication
WHERE title like :pattern OR publication_text like :pattern