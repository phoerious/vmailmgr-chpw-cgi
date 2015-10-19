<form action="{$formaction}" method="post">
    <div id="PasswordForm">
        <p><label for="accountname">Mail Account Name:</label>
        <input type="text" name="accountname" id="accountname" placeholder="Your account name, including internal prefix" required></p>
        <p><label for="oldpass">Old Mail Password:</label>
        <input type="password" name="oldpass" id="oldpass" required></p>
        <p><label for="newpass">New Mail Password:</label>
        <input type="password" name="newpass" id="newpass" required></p>
        <p><label for="newpass2">Repeat New Mail Password:</label>
        <input type="password" name="newpass2" id="newpass2" required></p>
        <p><input type="submit" name="submit" value="Change Password"></p>
    </div>
</form>
