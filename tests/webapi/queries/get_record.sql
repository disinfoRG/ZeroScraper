-- :name get_record :one
SELECT *
FROM play_record
WHERE
  publication_id = UNHEX(:publication_id)
AND play_at = :play_at
