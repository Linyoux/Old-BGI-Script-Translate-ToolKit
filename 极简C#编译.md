1. **安装最小依赖包**  
   下载微软官方轻量级[Build Tools](https://aka.ms/vs/17/release/vs_BuildTools.exe)，安装时：
   - 勾选 ".NET Framework 3.5 开发工具"
   - 勾选 "MSBuild"

2. **打开编译环境**  
   在开始菜单找到：  
   `Visual Studio 2022` → `x86 Native Tools Command Prompt`  
   （会自动配置环境变量）

3. **执行编译**  
   ```bash
   cd 你的项目目录
   msbuild /p:Configuration=Release
   ```
