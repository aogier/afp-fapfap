# AFP FAP FAP
last: 20160518

AFP FAP FAP (_**A**pple **F**ile **P**rotocol **F**ilenames **a**nd **P**athnames **F**ix **a**nd **P**reserve_) is a mass renamer for the mess the switch AFP -> SMB left on our fileservers.

It will be a tool we will use to cleanup some problem/oddities that currently block people's work.

### Please note that while we release this you can always access fileserver via FTP:// and fix things by yourself at [redacted].


## Which problems are addressed

As Apple unilaterally dropped AFP support from their operating system, a switch from AFP:// based file sharing to SMB://became more and more urgent and we finally made that campus-wide on April 11 2016.    
Unfortunately, as soon as lot of you started to use the new SMB:// protocol, strange things began to happen, mainly:

 * **permission-related issues when navigating files**
 * **empty folder that you know aren't empty**


## Causes

Since none of those errors is really true server side (eg. *we didn't loose any of your data, we didn't loose control on permission flows*), we took some time to analyze the situation in order to collect a matrix of causes for those issues.

What we have found is a few things we have to fix with stored data. Some problems are machine generated (metadata, system files), others are user-made poor choices (slashes in *file names*, multiple files w/ same name and different amount of trailing spaces ...)


Here is the matrix:


<table>
  <tr>
    <th rowspan="2" style="vertical-align: middle; text-align: center;">Problem</th>
    <th colspan="2" style="vertical-align: middle; text-align: center;">Operating System</th>
    <th rowspan="2" style="vertical-align: middle; text-align: center;">CAUSES</th>
    <th colspan="2" style="vertical-align: middle; text-align: center;">WILL BE</th>
  </tr>
  <tr>
    <th style="vertical-align: middle; text-align: center;">OSX</th>
    <th style="vertical-align: middle; text-align: center;">Windows</th>
    <th style="vertical-align: middle; text-align: center;">DELETED</th>
    <th style="vertical-align: middle; text-align: center;">RENAMED</th>
  </tr>
  <tr>
    <td>single file disappeared</td>
    <td style="vertical-align: middle; text-align: center;"><h3>&#10003;</h3>(10.10)</td>
    <td></td>
    <td>
      <ul>
        <li>trailing space in name "file "</li>
        <li>"slash" in name "file:2efname"</li>
        <li>"dot" in name "file:2ename"</li>
      </ul>
    </td>
    <td></td>
    <td style="vertical-align: middle; text-align: center;"><h3>&#10003;</h3></td>
  </tr>
  <tr>
    <td>see the file, cannot open</td>
    <td style="vertical-align: middle; text-align: center;"><h3>&#10003;</h3>(10.8)</td>
    <td style="vertical-align: middle; text-align: center;"><h3>&#10003;</h3></td>
    <td>
      <ul>
        <li>trailing space in name "file "</li>
        <li>"slash" in name "file:2efname"</li>
        <li>"dot" in name "file:2ename"</li>
      </ul>
    </td>
    <td></td>
    <td style="vertical-align: middle; text-align: center;"><h3>&#10003;</h3></td>
  </tr>
  <tr>
    <td>single folder disappeared</td>
    <td style="vertical-align: middle; text-align: center;"><h3>&#10003;</h3>(10.10)</td>
    <td></td>
    <td>
      <ul>
        <li>trailing space in name "folder "</li>
        <li>"slash" in name "file:2efname"</li>
        <li>"dot" in name "file:2ename"</li>
      </ul>
    </td>
    <td></td>
    <td style="vertical-align: middle; text-align: center;"><h3>&#10003;</h3></td>
  </tr>
  <tr>
    <td>see the folder, cannot open</td>
    <td></td>
    <td style="vertical-align: middle; text-align: center;"><h3>&#10003;</h3></td>
    <td>
      <ul>
        <li>trailing space in name "folder "</li>
        <li>"slash" in name "file:2efname"</li>
        <li>"dot" in name "file:2ename"</li>
      </ul>
    </td>
    <td></td>
    <td style="vertical-align: middle; text-align: center;"><h3>&#10003;</h3></td>
  </tr>
  <tr>
    <td>folder is empty</td>
    <td style="vertical-align: middle; text-align: center;"><h3>&#10003;</h3>(10.8)</td>
    <td></td>
    <td>
          <ul>
        <li>trailing space in name "folder "</li>
        <li>"slash" in name "file:2efname"</li>
        <li>"dot" in name "file:2ename"</li>
      </ul>
    </td>
    <td></td>
    <td style="vertical-align: middle; text-align: center;"><h3>&#10003;</h3></td>
  </tr>
  <tr>
    <td>cannot remove empty folder</td>
    <td style="vertical-align: middle; text-align: center;"><h3>&#10003;</h3></td>
    <td style="vertical-align: middle; text-align: center;"><h3>&#10003;</h3></td>
    <td>
          <ul>
        <li>:2eDS_Store</li>
      </ul>
    </td>
    <td style="vertical-align: middle; text-align: center;"><h3>&#10003;</h3></td>
    <td></td>
  </tr>
</table>

## Please note that there will probably be other oddities we have't tracked so far so this list will be updated (check date under title)

## Cleaning actions

Following cleaning actions will be taken:

 * trailing, leading spaces => **removed, 'file ' will become 'file'**
 * slash in filename => **become underscore, 'file/name' will become 'file_name'**
 * trailing, leading dot => **become a real dot, ':2efile' will become '.file'**
 * :2eDS_Store files => **DELETED (because useless ATM)**
