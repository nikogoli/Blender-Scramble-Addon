
# Blender-Scramble-Addon　(poll() のチェック用)

各機能のボタン有効化・実行条件を統一された形式に修正するための補助ブランチ
　
　

### いまのところのルール
* 原則として、メニューには条件を設けない　
　→　実行できない状態の場合は、項目を無効化(グレイアウト)する
* できる限り、エラーメッセージの表示ではなく、ボタンの無効化で対応する　
　⇔　機能名・説明文では条件がわかりにくい場合はエラーメッセージを使う
* 原則として、パネルでの非表示処理をボタンの無効化の代替として利用しない　
　→　パネルでの非表示は、「非対応のモード」・「操作対象なし」の場合に使用する　
　(⇔　コピー系の機能はどうすべき？)


### いまところのコードの記述ルール
* None との比較は明示する
* True/False との比較は明示しない　
* できる限り context を利用し、アクティブオブジェクトを経由しない
* (いちいち変数に代入しない)