-- :name update_publication_play_time :affected
UPDATE publication
SET
    play_count = play_count + 1,
    last_play_at = :last_play_at,
    first_play_at = IF(first_play_at IS NULL, :last_play_at, first_play_at)
WHERE
    publication_id = UNHEX(:publication_id);