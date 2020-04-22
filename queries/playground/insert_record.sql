-- :name insert_record :affected
INSERT INTO play_record
    (publication_id, play_at, content)
values
    (UNHEX(:publication_id), :play_at, :content);