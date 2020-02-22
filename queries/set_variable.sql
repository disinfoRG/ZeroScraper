-- :name set_variable :insert
INSERT Variable
VALUES
  (:key, :value)
ON DUPLICATE KEY UPDATE
  Variable.key = :key, value = :value
