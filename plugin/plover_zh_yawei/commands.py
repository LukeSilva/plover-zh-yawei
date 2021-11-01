def pick_char(ctx, cmdline):
    print("pick_char entry")
    action = ctx.copy_last_action()
    # {:del_char:N}
    args = cmdline.split(':')


    try:
        N = int(args[0])
    except IndexError:
        print("failed to get argument", args)
        return action


    print(action)

    action.text = action.word[N]
    action.prev_replace = action.word
    action.prev_attach = True

    print(action)
    return action
