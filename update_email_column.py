from app.core.db import engine
from sqlalchemy import text

# 更新用户表的email列，使其允许为空
with engine.connect() as conn:
    # 开始事务
    trans = conn.begin()
    try:
        # 修改email列，使其允许为空
        conn.execute(text('ALTER TABLE "user" ALTER COLUMN email DROP NOT NULL'))
        
        # 提交事务
        trans.commit()
        print('Table updated successfully')
    except Exception as e:
        # 回滚事务
        trans.rollback()
        print(f'Error updating table: {e}')