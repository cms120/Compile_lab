1. 代码实现后要写test再跑一下，在src/test/目录下面，不跑test，还是有挺多问题

   - 在test_cast.py文件下加一点测试样例，比如

   - ```python
     fa_s = [  # TODO
         [  # on ppt 3_2 page22
             ['S', 'Q', 'U', 'V', 'Z', 'phi'],
             ['0', '1'],
             [(('S', '0'), ['V', 'Q']),
              (('S', '1'), ['U', 'Q']),
              (('U', '0'), ['phi']),
              (('U', '1'), ['Z']),
              (('V', '0'), ['Z']),
              (('V', '1'), ['phi']),
              (('Q', '0'), ['V', 'Q']),
              (('Q', '1'), ['U', 'Q']),
              (('Z', '0'), ['Z']),
              (('Z', '1'), ['Z'])],
     
             'S',
             ['Z']
         ],
         [
             ['S', 'Z'],
             ['a']
         ]
     ]  # 用来测试确定化
     ```

     这个样例只写了一个，是ppt上的，第二个写了一半，需要再加几个

   - ```python
     def test_fa_2_dfa(self):
       self.assertTrue(True)
       for k, letters, f, s, z in fa_s:
         fa = FA(k, letters, f, s, z)
         print(fa_2_dfa(fa))
     ```

   - 运行的时候构建一下FA，然后看下结果，要是都跑不完，那就确定有问题了

   - 然后尽量多写几个样例跑一下

2. 写代码的时候在README.md里顺便把报告写了，就是讲代码思路的，这个以后也要写，现在写的话方便自己整理思路，别人看代码也快一点。

3. 这个已经过了一周了，还有三周交，留出一周处理边界问题，写报告，准备汇报；一周多写语法分析，时间已经有点紧了，那就**半周内把确定化和最小化写完，测试样例都过差不多，就是下周四之前，再拖后面的也不好进行了**。然后代码能跑过几个测试样例就可以。c--的我和乐天跑一下然后调试吧，因为前面是我们写的你们可能不熟悉。

4. 语法分析自顶向下要简单点应该，我们就先实现这个，然后带回溯的版本比较好理解，就是穷举，但是实现可能也不会多轻松，也比较慢，资料也比较少。我们就实现LL(1)吧，这个也比较好分工点，有比较多小步骤。

5. 我和乐天把语法分析大概构思写个框架，然后尽量把代码分相互之间少一些关联，这样我们之后写的时候可以分开写，也可以分开测试自己的部分，不会影响别人。你们写完测完之后，再接着写语法的部分。然后我和乐天来测c--的词法分析

