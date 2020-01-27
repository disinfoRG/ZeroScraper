-- :name delete_variable :affected
DELETE IGNORE
FROM Variable
WHERE Variable.key = :key
