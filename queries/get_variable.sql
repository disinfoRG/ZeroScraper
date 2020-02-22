-- :name get_variable :one
SELECT *
FROM Variable
WHERE Variable.key = :key
