-- :name get_publication_by_like :many
SELECT *
FROM publication
WHERE MATCH(title, publication_text) AGAINST (:query IN BOOLEAN MODE)
