# BGI 游戏翻译工具集

本项目通过一个核心批处理脚本 `_Process.bat` 整合了 BGI (Buriko General Interpreter) 引擎游戏的脚本解包、封包及文件整理步骤，旨在提供一个自动化、高效的本地化工作流。

## 目录结构与准备工作

为确保工具正常运行，请按以下结构组织您的项目文件夹：

1.  **提取脚本**: 使用解包工具（如 [GARbro](https://github.com/crskycode/GARbro)）从游戏资源包（例如 `data.arc`）中提取脚本文件。
2.  **组织文件**:
      * `_Process.bat`: **核心处理脚本**，所有操作都通过它执行。
      * `Tools/`: 存放 `ScriptDecoder.exe` 和 `ScriptEncoder.exe`。
      * `0_GARbro_Output/`: 存放从游戏中提取的**原始脚本文件**。这些文件通常没有文件后缀名，请直接将它们放入此文件夹。
      * `1_Decoded_TXT/`: 解包后生成的 `.txt` 文件将存放于此。
      * `2_Translated_TXT/`: 存放**翻译完成**的 `.txt` 文件。
      * `3_Encoded_Scripts/`: 封包后生成的临时脚本 (`.new` 后缀) 将存放于此。
      * `4_Final_Scripts/`: 存放最终可用于游戏测试的脚本。

## 核心工作流

所有操作均通过运行 `_Process.bat` 并选择对应选项来完成。

### 1\. 解包脚本 (选项 1)

此步骤会将 `0_GARbro_Output/` 目录中的原始脚本解包为可供翻译的 `.txt` 文件，并输出到 `1_Decoded_TXT/` 目录。

### 2\. 翻译文本 (手动)

  * 使用您偏好的翻译工具（如 [GalTransl](https://github.com/xd2333/GalTransl)）处理 `1_Decoded_TXT/` 目录中的文件。
  * **重要提示**: 若使用 GalTransl 的 `DumpInjector` 工具，请在“正则表达式模式”中填入以下规则以正确提取文本（GalTransl\_DumpInjector 仅提取正则表达式第一个捕获组的内容）：
    ```regex
    <\d+,\d+,\d+>\s*([^\x00-\x7F].{3,})
    ```
  * 将翻译完成的 `.txt` 文件放入 `2_Translated_TXT/` 目录。

### 3\. 封包脚本 (选项 2)

此步骤会整合 `0_GARbro_Output/` 的原始脚本与 `2_Translated_TXT/` 的翻译文本，生成带 `.new` 后缀的新脚本，并输出到 `3_Encoded_Scripts/` 目录。

### 4\. 清理文件 (选项 3)

此步骤会移除 `3_Encoded_Scripts/` 中文件的 `.new` 后缀，并将最终脚本输出到 `4_Final_Scripts/` 目录。

### 5\. 应用与测试 (手动)

BGI 引擎支持免封包读取，这意味着您无需将修改后的脚本重新打包回原始的 `.arc` 压缩包。

1.  **直接测试**: 将 `4_Final_Scripts/` 文件夹中的所有最终脚本文件，直接复制到**游戏可执行文件（.exe）所在的根目录**。启动游戏即可看到汉化效果。
2.  **打包发布 (可选)**: 为了方便分发补丁，您可以使用 [Molebox](https://github.com/sudachen/Molebox) 等工具，将游戏主程序（.exe）和所有翻译后的脚本文件打包成一个**新的独立可执行文件**。

## 关于工具的修改与编译

  * **原始工具**: `ScriptDecoder` 和 `ScriptEncoder` 基于 [xupefei/BGIKit](https://github.com/xupefei/BGIKit)。
  * **核心修改**: 为了让脚本能被日文原版游戏直接读取，本项目中的 `ScriptEncoder` 已将输出编码从 `GBK (CP936)` 修改为 `Shift-JIS (CP932)`。
  * **编译方法**:
    1.  安装 Visual Studio Build Tools，并确保勾选了 **".NET Framework 3.5 开发工具"** 和 **"MSBuild"**。
    2.  从开始菜单打开 `x86 Native Tools Command Prompt`。
    3.  进入项目源码目录，执行 `msbuild /p:Configuration=Release` 命令即可完成编译。