-- :name activate_site :affected
update Site set is_active = 1
where site_id = :site_id