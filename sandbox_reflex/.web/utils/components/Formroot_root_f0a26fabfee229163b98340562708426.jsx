
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,getRefValue,getRefValues,isTrue} from "$/utils/state"
import {Root as RadixFormRoot} from "@radix-ui/react-form"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Formroot_root_f0a26fabfee229163b98340562708426 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);

    const handleSubmit_a97f21222726b8f51c402da8d5d2c626 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.login", ({ ["form_data"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (true) {
            $form.reset()
        }
    })
    


    return(
        jsx(RadixFormRoot,{className:"Root ",css:({ ["width"] : "100%" }),onSubmit:handleSubmit_a97f21222726b8f51c402da8d5d2c626},children)
    )
});
