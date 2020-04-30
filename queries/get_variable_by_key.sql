-- :name get_variable_by_key :one
SELECT *
FROM Variable
WHERE Variable.key = :key
