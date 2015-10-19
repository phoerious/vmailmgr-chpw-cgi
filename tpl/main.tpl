<!DOCTYPE html>
<html>
<head>
<title>Change Mailbox Password</title>
<meta charset="utf-8">
<style>
    html {
        font-family: Calibri, Cantarell, sans-serif;
        font-size: 110%;
    }

    h1 {
        font-weight: bold;
        font-size: 2rem;
        border-bottom: 1px solid #aaa;
        padding: 0 0 .5rem 0;
        margin: 0 0 2rem 0;
    }

    h2 {
        font-weight: bold;
        font-size: 1rem;
        margin: 0 0 1rem 0;
    }

    label {
        display: block;
        float: left;
        width: 13rem;
        text-align: right;
        padding: .3rem 1rem;
        color: #777;
    }

    input[type="text"], input[type="password"] {
        padding: .3rem;
        width: 22rem;

    }

    input[type="submit"] {
        margin-left: 15rem;
    }

    a {
        color: #009;
    }

    a:hover, a:focus {
        text-decoration: none;
    }

    #Main {
        margin: 3rem auto;
        padding: 1rem;
        width: 40rem;
        border: 1px solid #ccc;
        box-shadow: 3px 3px 15px #eee;
        border-radius: 3px;
    }

    .error p {
        margin-left: 2rem;
    }

    .error .message {
        color: #900;
        font-style: italic;
    }

    .error a {
        display: block;
        text-align: right;
    }
</style>
<body>
    <div id="Main">
        <h1>Change Mailbox Password</h1>
        {$main_content}
    </div>
</body>
</html>
