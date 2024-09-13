<div align="center" id="top"> 
  <img src="./.github/app.gif" alt="Dsg" />

  &#xa0;

  <!-- <a href="https://dsg.netlify.app">Demo</a> -->
</div>

<h1 align="center">Dsg</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/{{YOUR_GITHUB_USERNAME}}/dsg?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/{{YOUR_GITHUB_USERNAME}}/dsg?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/{{YOUR_GITHUB_USERNAME}}/dsg?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/{{YOUR_GITHUB_USERNAME}}/dsg?color=56BEB8">

  <!-- <img alt="Github issues" src="https://img.shields.io/github/issues/{{YOUR_GITHUB_USERNAME}}/dsg?color=56BEB8" /> -->

  <!-- <img alt="Github forks" src="https://img.shields.io/github/forks/{{YOUR_GITHUB_USERNAME}}/dsg?color=56BEB8" /> -->

  <!-- <img alt="Github stars" src="https://img.shields.io/github/stars/{{YOUR_GITHUB_USERNAME}}/dsg?color=56BEB8" /> -->
</p>

<!-- Status -->

<!-- <h4 align="center"> 
	🚧  Dsg 🚀 Under construction...  🚧
</h4> 

<hr> -->

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/{{YOUR_GITHUB_USERNAME}}" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

数据源比较简单，只选取了日频的基础行情，所以做的因子也比较简单，主要用于实现基本功能，接口可以上传任何pl.DataFrame形式的因子文件，不过还需要附上收益率，因为暂时没有数据接口去匹配个股的收益信息。

## :sparkles: Features ##

1、由于对polars不熟悉，所以适应了一段时间。在编写复杂因子的实现效率上，polars也许不如pandas方便。举例：没有行处理的方法，所以实现不了groupby.apply,也无法在分区函数中实现除内置函数以外的功能，做rolling_group_apply这种复杂操作甚至只能写for循环
2、Data.py用了baostock的免费数据接口获取了日频的行情数据，我只节选了2024年1月1日到2024年6月10日的全市场数据，因为这段时间zz500没有成分股调整。
3、factors.py写了几个因子，有中文注释不再展开。这些因子未必是有用的，个人认为只通过高开低收量做的手工因子不如直接放到RNN里去跑黑箱。另外这里也没有考虑行业标签等重要变量。相对来说A股长期是反转因子为主，所以动量的因子无论经过何种处理在日频以上级别依旧是一个负向因子。7个因子中最有效的是收益率峰度，其次是长短期动量相除再用十日成交量波动率做调整，这两个都是负向因子，也验证了上述经验。
4、measure.py提供了计算单因子表现和画图的功能，单因子的IC、ICIR、分组收益率（分5组）、选股换手率、最大回撤、多空累计收益曲线在输出中展示。正确的回测是用开盘价并计算滑点。这里只用了收盘价方便计算。


## :rocket: Technologies ##

polars，matplotlib
个人理解pandas在策略研究时效率更高。对流数据处理、高频交易，应当优先考虑polars

## :white_check_mark: Requirements ##

Before starting :checkered_flag:, you need to have [Git](https://git-scm.com) and [Node](https://nodejs.org/en/) installed.

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/{{YOUR_GITHUB_USERNAME}}/dsg

# Access
$ cd dsg

# Install dependencies
$ yarn

# Run the project
$ yarn start

# The server will initialize in the <http://localhost:3000>
```

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.


Made with :heart: by <a href="https://github.com/{{YOUR_GITHUB_USERNAME}}" target="_blank">{{YOUR_NAME}}</a>

&#xa0;

<a href="#top">Back to top</a>
