-- :name get_publication_by_id :one
SELECT *
FROM publication
WHERE
  publication_id = UNHEX(:publication_id)
