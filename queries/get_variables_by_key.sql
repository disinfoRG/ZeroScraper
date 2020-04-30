-- :name get_variables_by_key :many
SELECT *
FROM Variable
WHERE Variable.key = :key
