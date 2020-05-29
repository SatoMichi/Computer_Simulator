# Computer_Simulator
"コンピュータシステムの理論と実装"という本をもとにしてコンピューターを論理ゲートから構築しようという試み。
本の中では様々なん言語を使ってコンピューターの仕組みが分かるように説明されていたが、本プロジェクトはそのすべてをPythonで実装しようという試みである。

This project is computer simulator written by Python based on the content of Japanese version of "The Elements of Computing Systems"(Noam Nisan, Shimon Schocken). In the book, it did not use one particular language to explain the sturcture and principle of computer. The aim of this project is implementing Computer Simulator by using the knowledge in the book.


    * 基本の論理ゲートとしては参考書籍とは違いNOT、AND、ORを用いる。本来なら指定されたビット数のみで動くように設計するべきだが、
      いくつかの論理ゲートの実装は柔軟な実装にしたため１６ビットと書かれていても任意のビットで動作する。
      As a functional complete logic gates, used NOT, AND, OR instead of NAND,which is used in the referenced book. Although, the gate
      (function) name says "16bit", some function will work for arbital number of bits due to generalised implementation.

Reference lists:  
コンピュータシステムの理論と実装 ―モダンなコンピュータの作り方　オライリージャパン (2015/3/25)
