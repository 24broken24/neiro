create or replace function insert_futura_info() returns trigger 
	as 
	$ad_fi_trigger$
begin 
update futura set totalsum=totalsum+new.quantity*new.price
where futura.id = new .ID_Futura;
return NULL;
END 
$ad_fi_trigger$ LANGUAGE plpgsql;
create or replace function delete_futura_info() returns trigger 
as 
$del_fi_trigger$
begin 
update futura set totalsum=totalsum-old.quantity*old.price
where futura.id=old.ID_Futura;
return NULL;
END
$del_fi_trigger$ language plpgsql;
create trigger ins_futura_info after insert on futurainfo
for each row execute procedure insert_futura_info();
create trigger del_futura_info after insert on futurainfo
for each row execute procedure delete_futura_info();