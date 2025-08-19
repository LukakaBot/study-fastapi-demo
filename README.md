# study-fastapi-demo

## 项目介绍
这是一个使用FastAPI框架构建的示例项目，用于学习和演示FastAPI的各种功能。

## 开发环境设置
为了获得最佳的开发体验和代码提示功能，请确保安装了以下工具：

1. Python 3.12或更高版本
2. uv包管理器

### 安装依赖
```bash
uv sync
```

### 运行开发服务器
```bash
uv run python main.py
```

## 数据库配置
项目使用PostgreSQL数据库，需要先安装并配置PostgreSQL：

### 在macOS上安装PostgreSQL
```bash
# 使用Homebrew安装PostgreSQL
brew install postgresql

# 启动PostgreSQL服务
brew services start postgresql

# 创建数据库用户和数据库
createuser -s devuser
createdb -O devuser postgres
```

### 在Ubuntu/Debian上安装PostgreSQL
```bash
# 更新包列表
sudo apt update

# 安装PostgreSQL
sudo apt install postgresql postgresql-contrib

# 启动PostgreSQL服务
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 切换到postgres用户并创建数据库用户和数据库
sudo -u postgres createuser -s devuser
sudo -u postgres createdb -O devuser postgres
```

### 数据库连接配置
默认的数据库配置为：
```python
DATABASE_URL = "postgresql://devuser:devuser@localhost:5432/postgres"
```

请根据实际情况修改数据库连接信息。

### 数据库连接池配置
项目使用了SQLAlchemy的连接池来管理数据库连接，以提高性能和资源利用率：

- `pool_size=10`: 连接池大小，保持10个连接在池中
- `max_overflow=20`: 超出pool_size后最多创建的连接数
- `pool_pre_ping=True`: 在使用连接前检查其有效性
- `pool_recycle=3600`: 连接回收时间，1小时后回收连接

这些配置可以根据实际需求进行调整。

## 项目结构
```
app/
├── core/
│   └── db.py
├── router/
│   ├── api/
│   │   └── user.py
│   └── main.py
├── main.py
```

## 路由配置
路由配置在`app/router/main.py`文件中完成，使用FastAPI的APIRouter来组织和管理路由。

## 开发工具
为了改善代码提示和开发体验，项目包含了以下开发依赖：
- python-lsp-server: 提供语言服务器协议支持
- jedi: 提供代码补全和静态分析功能

建议在IDE中配置这些工具以获得最佳的开发体验。