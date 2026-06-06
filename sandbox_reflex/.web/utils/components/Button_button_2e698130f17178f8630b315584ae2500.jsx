
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_2e698130f17178f8630b315584ae2500 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_24a816532945a677e6992617c2e2e76f = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state____auth_state.sandbox_reflex___data_state____data_state.close_empty_equipe_alert", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{css:({ ["backgroundColor"] : "#800000", ["color"] : "white", ["cursor"] : "pointer", ["&:hover"] : ({ ["backgroundColor"] : "#A30000" }) }),onClick:on_click_24a816532945a677e6992617c2e2e76f},children)
    )
});
