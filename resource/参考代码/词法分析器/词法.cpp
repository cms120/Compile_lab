#include <iostream>
#include <cstring>
#include <cstdio>
#include <algorithm>
#include <stack>
#include <fstream>
using namespace std;
const int num_of_keyword =63;
const int num_of_MO = 10;
const int num_of_BO = 13;
const int num_of_D = 3;
const char keyword[80][12] = { "OR"," XOR","AND","VALUES","FLOAT","float","int","INT","LEFT ","INSERT" ,"JOIN" ,"UPDATE", "DELETE","WHERE"," AS","INSET","INTO","FROM","WHERE","SELECT",
"RIGHT"," MIN","MAX","AVG","SUM","UNION","ALL","GROUP BY","HAVING","DISTINCT","on","ON","ORDER BY","TRUE","FALSE","IS","NOT","NULL","values","left","order by",
"join","updete","delete","where","as","right","min","sum","max","all","avg","union","having","insert","from","select","group by","distinct","true","false","is","null" };
const char Monocular_Operator[20] = {'.','!','%','~','&','|','^','=','<','>'};   //单目运算符
const char Binocular_Operator[20][5] = {"++","--","&&","||","<=","!=","==",">=","+=","-=","*=","/=" ,"<=>" }; //双目运算符
const char Delimiter[20] = { ',','(',')' }; //界符
const char weizhi[20] = {'!','%','~','&','|','^','=','_','?'};
FILE* file_source = NULL;
ifstream input;
ofstream output;
/******************************************/

/******************************************/
char f(char str[])        //映射到一个字符来表示
{
	if (strcmp(str, keyword[0]) == 0)
		return 'b';
	if (strcmp(str, keyword[1]) == 0)
		return 'c';
	if (strcmp(str, keyword[2]) == 0)   //char  a
		return 'a';
	if (strcmp(str, keyword[3]) == 0)   //continue   o
		return 'o';
	if (strcmp(str, keyword[4]) == 0)
		return 'd';
	if (strcmp(str, keyword[5]) == 0)	//default    n
		return 'n';
	if (strcmp(str, keyword[6]) == 0)	//double   z
		return 'z';
	if (strcmp(str, keyword[7]) == 0)
		return 'e';
	if (strcmp(str, keyword[8]) == 0)	//float  y
		return 'y';
	if (strcmp(str, keyword[9]) == 0)
		return 'f';
	if (strcmp(str, keyword[10]) == 0)
		return 'i';
	if (strcmp(str, keyword[11]) == 0)  //int    h
		return 'h';
	if (strcmp(str, keyword[12]) == 0)	//include  p
		return 'p';
	if (strcmp(str, keyword[13]) == 0)
		return 'l';
	if (strcmp(str, keyword[14]) == 0)
		return 'm';
	if (strcmp(str, keyword[15]) == 0)
		return 'r';
	if (strcmp(str, keyword[16]) == 0)
		return 's';
	if (strcmp(str, keyword[17]) == 0)
		return 't';
	if (strcmp(str, keyword[18]) == 0)
		return 'v';
	if (strcmp(str, keyword[19]) == 0)
		return 'u';
	if (strcmp(str, keyword[20]) == 0)
		return 'w';
	if (strcmp(str, keyword[21]) == 0)     //iostream   k
		return 'k';
}

char state[100];
int len_state;
//char move[100][100];
char start;
char final[100];
int len_final;
bool is_FINAL[150];

struct NFA_set
{
	char set[100];
	int len = 0;
};
char buffer[100];
int buffer_size = 0;

NFA_set MOVE[100][100];

char N_state[100];
int N_len_state;
char N_start;
char N_final[100];
int N_len_final;
bool N_is_final[100];

NFA_set new_set[100];
int num_new_set = 0;
int dfa[150][150];
bool Isweizhi(char a)
{
	for (int i = 0; i <11 ; ++i)
	{
		if (weizhi[i] == a)
		{
			return true;
		}
	}
	return false;
}
bool float1(char a[])
{
	int i = 0;
	while (1)
	{
		if (a[i++] == '.')
			return true;
		if (i == 16)
			break;
	}
	return false;
}
bool IsInteger(char a)
{
	if (a >= '0' && a <= '9')
		return true;
	return false;
}
bool IsLetter(char a)
{
	if (a >= 'a' && a <= 'z')
		return true;
	if (a >= 'A' && a <= 'Z')
		return true;
	return false;
}
bool IsKeyword(char a[],int &da)
{
	int len = strlen(a);
	for (int j = 0; j < num_of_keyword; ++j)
	{
		if (strlen(keyword[j]) == len)
		{
			if (strcmp(keyword[j], a) == 0)
			{
				da = j;
				return true;
			}
		}
	}
	return false;
}
bool IsMO(char a,int &dada)
{
	for (int i = 0; i < num_of_MO; ++i)
	{
		if (Monocular_Operator[i] == a)
		{
			dada = i;
			return true;
		}
	}
	return false;
}
bool IsBO(char a[],int &dad)
{
	for (int i = 0; i < num_of_BO; ++i)
	{
		if (strcmp(Binocular_Operator[i], a) == 0)
		{
			dad = i;
			return true;
		}
			
	}
	return false;
}
bool IsDelimiter(char a)
{
	for (int i = 0; i < num_of_D; ++i)
	{
		if (Delimiter[i] == a)
			return true;
	}
	return false;
}
bool Is_In_state(char a)
{
	for (int i = 0; i < len_state; ++i)
	{
		if (a == state[i])
			return true;
	}
	return false;
}
bool Is_In_final(char a)
{
	for (int i = 0; i < len_final; ++i)
	{
		if (a == final[i])
			return true;
	}
	return false;
}
bool Is_in_set(char a, NFA_set temp)
{
	for (int i = 0; i < temp.len; ++i)
	{
		if (a == temp.set[i])
			return true;
	}
	return false;
}
void createNFA()
{

	int N;
	bool flag = true;   //是不是第一个
	char ch;    //用来读 文法左边的
	char nouse;
	char str[10];    //用来读 文法 右边的
	input.open("词法分析_文法.txt");
	input >> N;
	while (N--)
	{
		input >> ch >> nouse >> nouse >> str;
		if (flag)
		{
			start = ch;
			flag = false;
		}
		if (!Is_In_state(ch))
		{
			state[len_state++] = ch;
		}
		if (!Is_In_final(str[0]))
		{
			final[len_final++] = str[0];
		}
		if (strlen(str) > 1)
		{
			MOVE[ch][str[0]].set[MOVE[ch][str[0]].len++] = str[1];
		}
		else
		{
			//if(str[0]=='@')        //用@表示伊布熊
				//is_final[ch]=true;
			//else
			MOVE[ch][str[0]].set[MOVE[ch][str[0]].len++] = 'Y';  //终态
		}
	}
}
void showNFA()
{
	for (int i = 0; i < 100; ++i)
	{
		for (int j = 0; j < 100; ++j)
		{
			for (int k = 0; k < 100; ++k)
			{
				if (MOVE[i][j].set[k] != '#')
					cout << char(i) << " " << char(j) << " " << k << " " << MOVE[i][j].set[k] << endl;
			}
		}
	}
}
int Is_in(NFA_set temp)   //和已有的newset有没有重复的，有就返回重复的编号
{
	bool flag[100];
	bool flag1;
	for (int i = 0; i < temp.len; ++i)
	{
		flag[i] = false;
	}
	for (int i = 0; i < num_new_set; ++i)
	{
		for (int k = 0; k < temp.len; ++k)
		{
			for (int j = 0; j < new_set[i].len; ++j)
			{
				if (temp.set[k] == new_set[i].set[j])
				{
					flag[k] = true;
				}
			}
		}
		flag1 = true;
		for (int m = 0; m < temp.len; ++m)
		{
			if (flag[m] == false)
			{
				flag1 = false;
				break;
			}
		}
		if (flag1 == true)
			return i;
		for (int m = 0; m < temp.len; ++m)
		{
			flag[m] = false;
		}
	}
	return -1;
}
void get_closure(NFA_set& temp)    //得到一个完整的子集 
{
	for (int i = 0; i < temp.len; ++i)
	{
		for (int j = 0; j < MOVE[temp.set[i]]['@'].len; ++j)
		{
			if (!Is_in_set(MOVE[temp.set[i]]['@'].set[j], temp))
			{
				temp.set[temp.len++] = MOVE[temp.set[i]]['@'].set[j];
			}
		}
	}
}
bool Is_contained_Y(NFA_set temp)   //判断是否是终态
{
	for (int i = 0; i < temp.len; ++i)
	{
		if (temp.set[i] == 'Y')
			return true;
	}
	return false;
}
void NFA_to_DFA()
{
	num_new_set = 0;
	NFA_set work_set;
	NFA_set worked_set;
	work_set.set[work_set.len++] = start;
	worked_set.len = 0;
	stack<NFA_set> s;
	get_closure(work_set);
	s.push(work_set);
	new_set[num_new_set++] = work_set;
	for (int i = 0; i < 150; ++i)
	{
		for (int j = 0; j < 150; ++j)
		{
			dfa[i][j] = '-1';
		}
	}
	for (int i = 0; i < 150; ++i)
		is_FINAL[i] = false;
	if (Is_contained_Y(work_set))
		is_FINAL[num_new_set - 1] = true;
	while (!s.empty())
	{
		work_set = s.top();
		s.pop();
		for (int i = 0; i < len_final; ++i)
		{
			for (int j = 0; j < work_set.len; ++j)
			{
				for (int k = 0; k < MOVE[work_set.set[j]][final[i]].len; ++k)
				{
					if (MOVE[work_set.set[j]][final[i]].set[k] != '#' && MOVE[work_set.set[j]][final[i]].set[k] != 'Y' && !Is_in_set(MOVE[work_set.set[j]][final[i]].set[k], worked_set))
					{
						worked_set.set[worked_set.len++] = MOVE[work_set.set[j]][final[i]].set[k];
					}
					if (MOVE[work_set.set[j]][final[i]].set[k] == 'Y' && !Is_in_set(MOVE[work_set.set[j]][final[i]].set[k], worked_set))
					{
						worked_set.set[worked_set.len++] = 'Y';    //用Y表示终态
					}
				}
			}
			get_closure(worked_set);
			if (worked_set.len > 0 && Is_in(worked_set) == -1)
			{
				dfa[num_new_set - 1][final[i]] = num_new_set;
				s.push(worked_set);
				new_set[num_new_set++] = worked_set;
				if (Is_contained_Y(worked_set))
				{
					is_FINAL[num_new_set - 1] = true;
				}
			}
			if (worked_set.len > 0 && Is_in(worked_set) > -1 && final[i] != '@')
			{
				dfa[Is_in(work_set)][final[i]] = Is_in(worked_set);
			}
			worked_set.len = 0;
		}
	}
	/*
	for(int i=0;i<150;++i)
	{
		for(int j=0;j<150;++j)
		{
			if(dfa[i][j]!='-1')
				cout<<i<<" "<<char(j)<<":"<<dfa[i][j]<<endl;
		}
	}
	for(int i=0;i<num_new_set;++i)
	{
		if(is_final[i])
			cout<<i<<" :"<<endl;
	}*/
}



bool DFA(char str[])
{
	char now_state = 0;
	for (int i = 0; i < strlen(str); ++i)
	{
		now_state = dfa[now_state][str[i]];
		if (now_state == -1)
			return false;
	}
	if (is_FINAL[now_state] == true)
		return true;
	return false;
}
void scan()
{
	char str[100];
	char ch;
	int i, j;
	int point;
	int flag;

	ch = fgetc(file_source);
	bool finish = false;
	while (!finish)
	{
		flag = -1;
		point = 0;
		if (IsInteger(ch))     //多一个ch
		{
			flag = 1;
			str[point++] = ch;
			ch = fgetc(file_source);
			while (IsLetter(ch) || IsInteger(ch) || ch == '.')
			{
				flag = 1;
				str[point++] = ch;
				ch = fgetc(file_source);
			}
			str[point] = '\0';
		}
		
		if (flag == 1)
		{
			if (float1(str))
			{
				cout << str << "	" << "<FLOAT , " << str << ">" << endl;
				output << str << "	" << "<FLOAT , " << str << ">" << endl;
			}
				
				
			/*if (DFA(str))
			{
				cout << str << "	" << "<INT , " <<str<<">"<< endl;
				output << 3;
			}*/
			else
			{
				cout << str << "	" << "<INT , " <<str<<">"<< endl;
				output << str << "	" << "<INT , " << str << ">" << endl;
			}
			point = 0;
			flag = -1;
		}
		if (IsLetter(ch)|| ch=='_')
		{
			flag = 2;
			str[point++] = ch;
			ch = fgetc(file_source);
			while (IsLetter(ch) || IsInteger(ch)|| Isweizhi(ch))
			{
				flag = 2;
				str[point++] = ch;
				ch = fgetc(file_source);
			}
			str[point] = '\0';
		}
		if (flag == 2)
		{
			int temp;
			if (IsKeyword(str,temp))
			{
				cout << str << "	" << "<KW , " <<temp<<">"<< endl;
				output << str << "	" << "<KW , " << temp << ">" << endl;
			}
			else
			{
			/*	if (DFA(str))
				{
					cout <<"false" << endl;
					
				}
				else
				{*/
					cout << str << "	" << "<IDN , " <<str<<">"<< endl;
					output << str << "	" << "<IDN , " << str << ">" << endl;
				//}
			}
			point = 0;
			flag = -1;
		}
		if (ch == '"')     //多一个ch
		{
			flag = 3;
			str[point++] = ch;
			ch = fgetc(file_source);
			while (1)
			{
				flag = 3;
				str[point++] = ch;
				if (ch == '"')
					break;
				ch = fgetc(file_source);
			}
			str[point] = '\0';
			
		}
		if (flag == 3)
		{
			cout << str << "	" << "<STRING , " << str << ">" << endl;
			output << str << "	" << "<STRING , " << str << ">" << endl;
			if ((ch = fgetc(file_source)) == EOF)
			{
				finish = true;
				break;
			}
			point = 0;
			flag = -1;
		}
		/*while(IsInteger(ch) || ch=='.')
		{
			flag=2;
			str[point++]=ch;
			if((ch=fgetc(file_source))==EOF)
			{
				finish=true;
				break;
			}
		}
		str[point]='/0';
		if(flag==2)
		{
			if(DFA(str))
			{
				cout<<str<<" "<<"数字"<<endl;
				output<<3;
			}
			else
			{
				cout<<str<<" "<<"出错不是数字"<<endl;
			}
			flag=-1;
		}*/
		if (IsDelimiter(ch))
		{
			cout << ch <<"    " << "<SE, " << ch << ">" << endl;
			output << ch << "    " << "<SE, " << ch << ">" << endl;
			/*if (ch == '#')
				output << '*';
			else
				output << ch;*/
			if ((ch = fgetc(file_source)) == EOF)
			{
				finish = true;
				break;
			}
		}
		int a;
		if (IsMO(ch, a)&&ch!=' ')
		{
			int temp1;
			str[point++] = ch;
			if ((ch = fgetc(file_source)) == EOF)
			{
				finish = true;
				break;
			}
			str[point++] = ch;
			str[point] = '\0';
			if (finish == false && IsBO(str, temp1))
			{
				cout << str<< "    " << "< OP , " << temp1 << ">" << endl;
				output<< str << "    " << "< OP , " << temp1 << ">" << endl;
				ch = fgetc(file_source);
			}
			else
			{
				cout << str[0]<< "    " << "< OP , " << a << ">" << endl;
				output << str[0] << "    " << "< OP , " << a << ">" << endl;
			}
			point = 0;
			
		}
					
		if (ch == ' ' || ch == '\n' || ch == '\t')
		{
			if ((ch = fgetc(file_source)) == EOF)
			{
				finish = true;
				break;
			}
			continue;
		}
	}
	output << '#';
}
void init()
{
	len_final = 0;
	len_state = 0;
	for (int i = 0; i < 100; ++i)
	{
		//is_final[i]=false;
		for (int j = 0; j < 100; ++j)
			for (int k = 0; k < 100; ++k)
				MOVE[i][j].set[k] = '#';
	}
}
void show()
{
	for (int i = 0; i < num_new_set; ++i)
	{
		cout << i << "的set" << endl;
		for (int j = 0; j < new_set[i].len; ++j)
		{

			cout << new_set[i].set[j] << " ";
		}
		cout << endl;
	}
}
int main()
{
	init();
	len_final = 0;
	len_state = 0;
	file_source = fopen("词法分析_源程序.sql", "r+");
	output.open("D:\\编译原理答辩\\Blex.tsv");
	scan();
	fclose(file_source);
	output.close();
	return 0;
}