-- :name get_site_by_airtable_id :one
SELECT *
FROM Site
WHERE airtable_id = :airtable_id
