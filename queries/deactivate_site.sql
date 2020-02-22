-- :name deactivate_site :affected
update Site set is_active = 0
where site_id = :site_id