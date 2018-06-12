select
  (case when password = 'Welkom01' AND username = 'Timo' THEN 0 else 1 end)
from customerinfo
where username = 'Timo'

