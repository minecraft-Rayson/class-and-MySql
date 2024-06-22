// 初始化
#include <iostream>
#include <cstdlib>
#include <string>
using namespace std;

int main()
{
    // 输入歌曲名
    string musicname;
    cout << "请输入歌曲名: ";
    cin >> musicname;
    // 生成网页链接
    string web1 = "start https://music.163.com/#/search/m/?s=" + musicname;
    string web2 = "start https://www.kugou.com/yy/html/search.html#searchType=song&searchKeyWord=" + musicname;
    string web3 = "start https://y.qq.com/n/ryqq/search?w=" + musicname;
    // 打开网页
    system(web1.c_str());
    system(web2.c_str());
    system(web3.c_str());

    return 0;
}