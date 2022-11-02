; ModuleID = 'sysy2022_compiler'
source_filename = "../input/05_var_defn.sy"

@a = global i32 3
@b = global i32 1
@c = global i32 3
@e = global i32 0
@f = global i32 10
declare i32 @getint()

declare i32 @getch()

declare i32 @getarray(i32*)

declare void @putint(i32)

declare void @putch(i32)

declare void @putarray(i32, i32*)

declare void @starttime()

declare void @stoptime()

define i32 @main() {
main_ENTRY:
  %op0 = alloca i32
  store i32 5, i32* %op0
  %op1 = alloca i32
  store i32 2, i32* %op1
  %op2 = alloca i32
  %op3 = load i32, i32* @f
  %op4 = load i32, i32* @e
  %op5 = add i32 %op3, %op4
  store i32 %op5, i32* %op2
  %op6 = load i32, i32* @f
  %op7 = load i32, i32* @e
  %op8 = add i32 %op6, %op7
  %op9 = alloca i32
  %op10 = load i32, i32* @f
  %op11 = add i32 %op10, i32 2
  store i32 %op11, i32* %op9
  %op12 = load i32, i32* @f
  %op13 = add i32 %op12, i32 2
  %op14 = alloca i32
  %op15 = load i32, i32* %op1
  store i32 %op15, i32* %op14
  %op16 = load i32, i32* %op1
  %op17 = load i32, i32* %op0
  %op18 = load i32, i32* @b
  %op19 = add i32 %op17, %op18
  ret i32 %op19
}
