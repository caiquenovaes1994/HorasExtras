
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_13da9c128a8e5cc2a052f4c3fe141093 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_a92a9f10fa7f696810568dbcf2377807 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.baixar_pdf_equipe", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)



    return(
        jsx(RadixThemesButton,{color:"ruby",css:({ ["width"] : "100%" }),disabled:reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.is_generating_pdf_rx_state_,onClick:on_click_a92a9f10fa7f696810568dbcf2377807,variant:"outline"},children)
    )
});
