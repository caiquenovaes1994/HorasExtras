
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_0727f2b670c07d36d79b6e62367af46c = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_2ee991d9a72984dcb77aa543559c521e = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_hoteis____hotel_state.open_new_hotel", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{css:({ ["backgroundColor"] : "#2ecc71", ["color"] : "white", ["cursor"] : "pointer", ["&:hover"] : ({ ["backgroundColor"] : "#27ae60" }) }),onClick:on_click_2ee991d9a72984dcb77aa543559c521e},children)
    )
});
