
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,getRefValue,getRefValues,isTrue} from "$/utils/state"
import {Root as RadixFormRoot} from "@radix-ui/react-form"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Formroot_root_ae38c9b22cf2bbde8bc1c5ed04dc7f81 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);

    const handleSubmit_5e73f35d4f5a49163d274b93655f3019 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.reset_password", ({ ["form_data"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (true) {
            $form.reset()
        }
    })
    


    return(
        jsx(RadixFormRoot,{className:"Root ",css:({ ["width"] : "100%" }),onSubmit:handleSubmit_5e73f35d4f5a49163d274b93655f3019},children)
    )
});
