-- :name get_publication_by_match :many
SELECT *, MATCH (title, publication_text) AGAINST
    (:query IN NATURAL LANGUAGE MODE) AS score
FROM publication
WHERE MATCH (title, publication_text)
AGAINST (:query
    IN NATURAL LANGUAGE MODE)