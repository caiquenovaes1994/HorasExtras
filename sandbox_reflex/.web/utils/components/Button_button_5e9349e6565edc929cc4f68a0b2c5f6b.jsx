
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_5e9349e6565edc929cc4f68a0b2c5f6b = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_d1291449be5abcc160ee8a8078053110 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.baixar_pdf_individual", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)



    return(
        jsx(RadixThemesButton,{css:({ ["backgroundColor"] : "#800000", ["color"] : "white", ["width"] : "100%", ["marginBottom"] : "0.5em", ["&:hover"] : ({ ["backgroundColor"] : "#A30000" }) }),disabled:reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.is_generating_pdf_rx_state_,onClick:on_click_d1291449be5abcc160ee8a8078053110},children)
    )
});
