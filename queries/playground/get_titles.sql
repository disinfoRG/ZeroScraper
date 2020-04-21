-- :name get_titles :many
SELECT
    HEX(publication_id) as publication_id, title as text
FROM publication
ORDER BY
    play_count asc,
    last_play_at asc
LIMIT :limit;