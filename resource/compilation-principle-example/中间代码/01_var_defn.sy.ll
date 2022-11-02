; ModuleID = 'sysy2022_compiler'
source_filename = "../input/01_var_defn.sy"

@a = global i32 0
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
  %op0 = load i32, i32* @a
  store i32 %op0, i32 10
  ret i32 0
}
