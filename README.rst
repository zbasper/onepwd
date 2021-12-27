=======
onepwd
=======
加密保存个人所有用户名和密码

* 使用python3.10开发运行，在windows10和mac os 12系统上测试通过
* 使用AES加解密

安装说明
--------
windows
^^^^^^^
1. 下载源代码
2. 在源程序目录下运行安装脚本 ::

    > python3 setup.py

3. 在当前目录生成onepwd.vbs脚本，双击生成的vbs脚本，或将此脚本添加为桌面快捷方式

mac
^^^^^
1. 下载源代码
2. 如果指定的pip源不是pypi.python.org，在~.pip/pip.conf中增加一行 ::

    [install]
    trusted-host=<mirror.xx.com/simple-源镜像地址>

3. 在源程序目录下运行安装脚本 ::

    $ python3 setup.py

4. 在当前目录下生成onepwd.sh脚本。

5. 添加Automator应用程序

    - 从桌面底部Dock菜单栏的Launchpad中，找到Automator(自动操作)双击打开
    - 选择文档类型为Application(应用)
    - 找到Run Shell Script(运行shell脚本), 双击后在右侧显示一个输入窗口
    - 把生成的onepwd.sh脚本文件拖到输入窗口的文本框内，保存文件类型为Application(应用)

6. 双击该保存的Application(应用)文件即可运行。

使用说明
--------
* 在主窗口中点击add(快捷键 ``Command-a`` 或者 ``Alt-a`` )按钮，打开用户名、密码添加窗口。

  * key输入框，用来输入加解密用的密钥，务必记住该唯一密钥，这也是你必须记住的唯一密码。
  * title输入框，用来输入生活、工作、学习中所设用户名密码的出处描述，如某某邮箱，某某网站等。
  * username输入框，用来输入对应的登录用户名
  * password输入框，用来输入对应的密码

* 输入完成后，直接按回车键或点击add按钮，将输入信息添加到数据文件中，并清空输入框(保留key输入框的内容，全部的输入内容，均使用唯一的密钥加密，下次再输入时也要使用该密钥)。
* 点击return按钮(快捷键 ``Comand-r`` 或者 ``Alt-r`` )，返回主窗口，查看输入的经过加密的内容。
* 在主窗口的key输入框，输入唯一密钥，按回车键或点击decrypt按钮，解密显示输入的内容，再按回车键或点击recovery按钮，恢复加密显示。
* 数据保存在当前目录的data目录下

