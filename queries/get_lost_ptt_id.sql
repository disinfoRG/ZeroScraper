-- :name get_lost_ptt_id :many
SELECT article_id
FROM SnapshotLoss
WHERE url like "%ptt.cc%";

