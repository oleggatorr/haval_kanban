## models
### user_role
employee_id - `str(10)` - pk
role - `string`
global_permissions - `json`
create_at
update_at
is_active
remove_at

### project_board
id
name
description
positions
create_at
update_at
is_active
remove_at

### project_column
id
project_board.id
name
description
positions
create_at
update_at
is_active
remove_at

### project_card
project_column.id
project.id
positions
name
create_at
update_at
is_active
remove_at

### project
id
name
create_at
update_at
is_active
remove_at

### project_data
project.id 1 к 1
big_description
create_at
update_at
is_active
remove_at

-----------------------------------

### task_board
id
project.id 1 к 1
name
description
create_at
update_at
is_active
remove_at

### task_board_users
task_board.id
user_role.employee_id
permissions - `json`
role - `string`
create_at
update_at
is_active
remove_at

### task_column
id
task_board.id
name
description
flags
positions
create_at
update_at
is_active
remove_at

### task
id
task_column.id
name
description
positions
task_status.id
date_time_start
date_time_end
planing_date_time_start
planing_date_time_end
create_at
update_at
is_active
remove_at

### task_data
task.id 1 к 1
big_description
owner_id - user_role.employee_id
create_at
update_at
is_active
remove_at

### task_users
task.id
user_role.employee_id
create_at
update_at
is_active
remove_at

### sab_task
id
task.id
name
description
positions
task_status.id
date_time_start
date_time_end
planing_date_time_start
planing_date_time_end
create_at
update_at
is_active
remove_at

### sab_task_users
sab_task.id
user_role.employee_id
create_at
update_at
is_active
remove_at

### task_status
id
name
description
is_default
is_final
create_at
update_at
is_active
remove_at