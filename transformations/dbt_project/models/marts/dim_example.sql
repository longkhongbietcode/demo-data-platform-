-- Example marts model
select id, upper(name) as name_upper
from {{ ref('stg_example') }}
