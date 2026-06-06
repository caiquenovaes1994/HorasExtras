
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue,pyOr} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_d3a25beea4289c77495fb39abe2df0c6 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_a92a9f10fa7f696810568dbcf2377807 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.baixar_pdf_equipe", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state)



    return(
        jsx(RadixThemesButton,{color:"ruby",css:({ ["width"] : "100%" }),disabled:pyOr(reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.is_generating_pdf_rx_state_, () => ((reflex___state____state__sandbox_reflex___state____auth_state__sandbox_reflex___data_state____data_state.total_chamados_rx_state_?.valueOf?.() === 0?.valueOf?.()))),onClick:on_click_a92a9f10fa7f696810568dbcf2377807,variant:"outline"},children)
    )
});
